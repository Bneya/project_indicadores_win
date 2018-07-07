<?php

    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "registro";


    // VARIABLE QUE ALMACENA LA CONEXIÓN A LA DB
    $mysqli = new mysqli($servername, $username, $password, $dbname);

    if($mysqli->connect_errno) {
      die("Fallo en la conexión");
      
    } else {
      echo "Conexión exitosa!";
    }
?>
