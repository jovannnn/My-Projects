<?php
$servername = "localhost";
$username = "root";
$password = "Fikt_Bitola_EDU123";
$dbname = "forma";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Поврзувањето не успеа: " . $conn->connect_error);
}

$ime = $_POST['ime'];
$prezime = $_POST['prezime'];
$email = $_POST['email'];
$telefon = $_POST['telefon'];
$adresa = $_POST['adresa'];
$profesija = $_POST['profesija'];

$sql = "INSERT INTO forma (ime, prezime, email, telefon, adresa, profesija)
VALUES ('$ime', '$prezime', '$email', '$telefon', '$adresa', '$profesija')";

if ($conn->query($sql) === TRUE) {
    echo "Податоците се успешно зачувани!";
} else {
    echo "Грешка: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
