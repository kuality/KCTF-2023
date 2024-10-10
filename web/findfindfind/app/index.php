<?php 

require_once("config.php");

if(isset($_GET['id']) && isset($_GET['pw'])){
	$id = $_GET['id'];
	$pw = $_GET['pw'];

	if ( preg_match("/,/is", $id )||preg_match("/,/is", $pw) ){ die("hack!"); }

	$query = $conn->query("SELECT upw FROM users WHERE uid='$id' and upw='$pw';");
	$result = $query->fetch_assoc();

	if($pw == $result['upw']) { echo $flag; }
	else { echo "empty!"; }
}

highlight_file(__FILE__);

?>
