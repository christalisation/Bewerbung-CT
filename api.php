<?php

include 'credentials.php';
$pdo_CT = new PDO('mysql:host=localhost;dbname=CT_data;charset=UTF8;', $login, $pass);
// Warning: charset=UTF8 very important parameter for the json_encode

$response = array();

set_time_limit(0);

function waitforchange($nof) {
    clearstatcache();
    $lfilemod=$nof;
    while($nof == $lfilemod) {
        clearstatcache();
        usleep(10000);
    }
}

if($pdo_CT == NULL){
    echo "Database connecton failed.";

}else{

    header("Content-Type: JSON");
    $query = "SELECT * FROM cdb_person
        JOIN cdb_gemeindeperson 
        ON cdb_person.id = cdb_gemeindeperson.person_id";
    $statement = $pdo_CT->prepare($query);
    $statement->execute();
    $request = $statement->fetchAll(PDO::FETCH_ASSOC);
    // $request = array();
    // $a = 0;
    // while ($a <= 2) {
    //     $request[$a]= $statement->fetch(PDO::FETCH_ASSOC);
    //     $a++;
    // }
    // var_dump($request);
    // print_r($request);
    $json = json_encode($request, JSON_PRETTY_PRINT);
    if (!$json){
        echo 'Error with json_encode.';
    }

    $file = fopen('table.json','w');
    fwrite($file, $json);
    fclose($file);

    // $tmp = shell_exec("record_linkage.py");
    // while(!$tmp) {
    //     sleep(10);
    // }
    $output=null;
    // $retval=null;
    // exec('record_linkage.py', $output, $retval);
    // echo "Returned with status $retval and output:\n";
    $command = 'record_linkage.py';
    $output = shell_exec($command);
    echo $output;

    // echo($json);
}

?>