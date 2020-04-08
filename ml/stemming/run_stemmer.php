<?php

require_once('RomanianStemmer.php');


foreach($argv as $arg) {
    echo RomanianStemmer::stem($arg)."\n";
}

?>
