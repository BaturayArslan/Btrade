<?php
$data = json_decode(file_get_contents('php://input'), true);
$data["id"] = rand(0,999999999);
$data["time"] = time();
$jsonObject = json_encode($data);

file_put_contents("/var/www/webhook/event.txt", $jsonObject);



?>
