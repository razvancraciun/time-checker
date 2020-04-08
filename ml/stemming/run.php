<?php

require_once('RomanianStemmer.php');


foreach(array_slice($argv, 1) as $arg) {
    echo RomanianStemmer::stem($arg)."\n";
}
