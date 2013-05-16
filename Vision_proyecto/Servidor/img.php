<?php
/*
    Codigo que carga imagenes al servidor para mandar llamar al puerto socket
*/
      $archivo = basename($_FILES['userfile']['name']);
      $path = "uploads/". $archivo;

   if (move_uploaded_file($_FILES['userfile']['tmp_name'], $path)) {
          $host = "127.0.0.1";
          $port = 6699;
          $msj = $archivo;
          $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
          $resp = socket_connect($socket, $host, $port) or die("Could not connect to server\n");  
          socket_write($socket, $msj, strlen($msj)) or die("Could not send data to server\n");
          $resp = socket_read ($socket, 1024) or die("Could not read server response\n");
          echo "Le has atinado un ". $resp ."%";
          socket_close($socket);
    }

?>