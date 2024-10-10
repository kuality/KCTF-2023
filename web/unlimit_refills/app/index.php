<?php 


require_once './flag.php';


if ( $_SERVER['REMOTE_ADDR'] == '127.0.0.1' )	 echo $flag;
else {
	if(isset($_GET['page'])){ require_once($_GET['page']); }
}

highlight_file(__FILE__);

?>
