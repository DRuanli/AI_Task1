<?php
$error = '';
$pass = '';
$email = '';

if (isset($_POST['email']) && isset($_POST['pass'])){
    $email = $_POST['email'];
    $pass = $_POST['pass'];

    if($email === '')
        $error = 'Please enter your email';
    else if($pass === '')
        $error = 'Please enter your password';
    else if(strlen($pass) < 6)
        $error = 'The password is not complex enough';
    else if($email !== 'admin@gmail.com' || $pass !== '123456')
        $error = 'Your email or password is not correct';
    else
        header('Location: /dashboard');
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }

        .login-container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }

        .login-container h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        .login-container input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .login-container button {
            width: 100%;
            padding: 10px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        .login-container button:hover {
            background: #218838;
        }
        
        .error{
            padding: 1px; 
            margin-left: 2px;
            color: red;
            font-size: 10px;
        }
    </style>
</head>

<body>
    <div class="login-container">
        <h2>Login</h2>
        <form action='' method='POST'>
            <input value="<?= $email ?>" name="email" type="email" placeholder="Email">
            <input value="<?= $pass ?>" name="pass" type="password" placeholder="Password">
            <button type="submit">Login</button>
            <p class="error"><?= $error ?></p>
        </form>
    </div>
</body>

</html>