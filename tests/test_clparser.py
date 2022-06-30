import pytest
from adapter import Adapter
from console.clparser import Parser
from wrappers.kucoin import Kucoin
from session import Session
import exception
from typing import Type
from pathlib import Path


@pytest.fixture
def set_config_file(tmp_path: Type[Path]):
    content = '''
        [secrets]
        key = test_purpose
        secret= some_random_secret_1231
        passphrase= wqqKJEr3
    '''

    d: Type[Path] = tmp_path / "btrade"
    d.mkdir()
    p: Type[Path] = d / "config.ini"
    p.write_text(content)

    return p


class TestCLParser:

    @pytest.mark.parametrize(
        "options,session,expected",
        [
            ([('-p', '20'), ('-s', '10'), ('-l', '20'), ('--pair', 'XBTUSDM'),
              ('-e', 'kucoin'), ('-f', '')], {}, exception.EmptyArgument),

            ([('-p', '20'), ('-s', '10'), ('-l', ''), ('--pair', 'XBTUSDM'),
              ('-e', 'kucoin'), ('-f', './config.ini')], {}, exception.EmptyArgument),

            ([('-p', '20'), ('--pair', 'XBTUSDM'),
              ('-e', 'kucoin'), ('-f', './config.ini')], {}, exception.BadArgumentNumber),

            ([('-p', 'merhaba'), ('-s', '10'), ('-l', 'hello'), ('--pair', 'XBTUSDM'),
             ('-e', 'kucoin'), ('-f', './config.ini')], {}, exception.BadArgumentType),

            ([('-p', '20'), ('-s', '10'), ('-l', '20'), ('--pair', 'XBTUSDM'),
              ('-e', 'SALLAMA'), ('-f', './config.ini')], {}, exception.BadArgumentValue),

        ],
    )
    def test_validate_1(self, options, session, expected: Type[Exception]):
        parser = Parser()

        with pytest.raises(expected) as e:
            parser._validate(options, session)
        assert e.type == expected

    @pytest.mark.parametrize(
        "options,session,expected",
        [
            (
                [('-p', '20'), ('-s', '10'), ('-l', '20'), ('--pair', 'XBTUSDM'),
                 ('-e', 'kucoin'), ('-f', './config.ini')],
                Session(),
                dict(
                    leverage=20,
                    profit_trashold=20,
                    loss_trashold=10,
                    pair="XBTUSDM",
                    exchange="kucoin",
                    key="",
                    secret="",
                    passphrase=""
                )
            )
        ]
    )
    def test_validate_2(self, options, session: Type[Session], expected):
        parser = Parser()
        parser._validate(options, session)
        assert session.get() == expected

    def test_parse(self, set_config_file):
        p = set_config_file

        arguments = ['-p', '20', '-s', '10', '-l', '10',
                     '--pair', 'XBTUSDM', '-e', 'kucoin', '-f', str(p)]
        session = Parser().parse(arguments)

        assert session["key"] == "test_purpose"
        assert session["secret"] == "some_random_secret_1231"
        assert session["passphrase"] == "wqqKJEr3"
        assert isinstance(session["api"], Adapter)
        assert isinstance(session["api"].get(), Kucoin)
