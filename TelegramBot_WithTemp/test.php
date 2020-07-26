
<?php  
exec('modprobe w1-gpio');
exec('modprobe w1-therm');

$device_file = '/sys/bus/w1/devices/28-031664445cff/w1_slave';
$data = file($device_file, FILE_IGNORE_NEW_LINES);
$temperature = null;

$device_file1 = '/sys/bus/w1/devices/28-041663868bff/w1_slave';
$data1 = file($device_file1, FILE_IGNORE_NEW_LINES);
$temperature1 = null;


if (preg_match('/YES$/', $data[0])) {
    if (preg_match('/t=(\d+)$/', $data[1], $matches, PREG_OFFSET_CAPTURE)) {
        $temperature = $matches[1][0] / 1000;
    }
}

if (preg_match('/YES$/', $data1[0])) {
    if (preg_match('/t=(\d+)$/', $data1[1], $matches, PREG_OFFSET_CAPTURE)) {
        $temperature1 = $matches[1][0] / 1000;
    }
}


if ($temperature) {
    echo "Temperature1 is ${temperature}C\n";
} else {
    echo "Unable to get temperature\n";
}

if ($temperature1) {
    echo "Temperature2 is ${temperature1}C\n";
} else {
    echo "Unable to get temperature1\n";
}


$con=mysqli_connect("localhost","root","newdvbt2","pi");
mysqli_set_charset($con,'utf8');
$sql="SELECT * FROM `text` ORDER BY `text` DESC";
$result=mysqli_query($con,$sql);
$arr=mysqli_fetch_all($result,MYSQLI_ASSOC);

function gog($x)
{
	echo "<pre>";
	print_r($x);
	echo "</pre>";
}
?>

<html>
<head>
<meta name="viewport" content="width=device-width" />
<?php
$i=0;
while ($i<count($arr)) {
        ?>

<title>Controller</title>
<link rel="shortcut icon" href="./<?php echo $arr[$i]['img']  ?>">

<?php
        $i++;
}

?>
    
</head>
<body>
<?php
$i=0;
while ($i<count($arr)) {
	?>
<h1><?php echo $arr[$i]['text']  ?></h1>
<?php
	$i++;
}

?>
        <form method="get" action="test.php">
             <input type="submit" value="ON" name="on">
              <input type="submit" value="OFF" name="off">
       </form>
      <?php
       $setmode6 = shell_exec("/usr/local/bin/gpio -g mode 6 out");
       if(isset($_GET['on'])){
               $gpio_on = shell_exec("/usr/local/bin/gpio -g write 6 1");
              echo "LED is on";
       }
      else if(isset($_GET['off'])){
                $gpio_off = shell_exec("/usr/local/bin/gpio -g write 6 0");
               echo "LED is off";
}
?>
</body>
</html>
