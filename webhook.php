<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


// Database connection details
$host = "localhost"; // Hostname for XAMPP
$user = "root";      // Default MySQL username
$password = "";      // Default MySQL password (leave blank for XAMPP)
$dbname = "chatbot_backend"; // Database name

// Connect to the database
$conn = new mysqli($host, $user, $password, $dbname);

// Check for a database connection error
if ($conn->connect_error) {
    http_response_code(500); // Internal Server Error
    echo json_encode(["fulfillmentText" => "Database connection failed."]);
    exit();
}

// Retrieve the request body sent by Dialogflow
$requestBody = file_get_contents("php://input");
$requestJson = json_decode($requestBody, true);

// Extract the intent name from the Dialogflow request
$intent = $requestJson['queryResult']['intent']['displayName'] ?? '';

// Initialize a default response
$responseText = "Sorry, I couldn't understand your question. Please try again.";

// Query the database for a response to the intent
if (!empty($intent)) {
    $stmt = $conn->prepare("SELECT response FROM intents_responses WHERE intent_name = ?");
    $stmt->bind_param("s", $intent);
    $stmt->execute();
    $result = $stmt->get_result();

    // Check if a response was found for the intent
    if ($row = $result->fetch_assoc()) {
        $responseText = $row['response'];
    }
    $stmt->close();
}

// Build the response for Dialogflow
$response = [
    "fulfillmentText" => $responseText // The response text sent back to Dialogflow
];

// Send the response back as JSON
header("Content-Type: application/json");
echo json_encode($response);

// Close the database connection
$conn->close();
?>
