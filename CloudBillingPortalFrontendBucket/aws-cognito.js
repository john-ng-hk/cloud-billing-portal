// AWS Cognito configuration done by deploy.sh

// Initialize the Amazon Cognito credentials provider
AWS.config.region = region;

// Handle login
document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    document.getElementById('loginMessage').textContent = 'Logging in...';

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const authenticationData = {
        Username: username,
        Password: password,
    };
    const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);
    const poolData = {
        UserPoolId: userPoolId,
        ClientId: clientId,
    };
    const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    const userData = {
        Username: username,
        Pool: userPool,
    };
    const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            console.log('Login successful:', result);
            document.getElementById('loginMessage').textContent = 'Login successful! Redirecting...';
            AWS.config.credentials = new AWS.CognitoIdentityCredentials({
                IdentityPoolId: identityPoolId,
                Logins: {
                    [`cognito-idp.${region}.amazonaws.com/${userPoolId}`]: result.getIdToken().getJwtToken(),
                },
            });
            AWS.config.credentials.refresh((error) => {
                if (error) {
                    console.error(error);
                } else {
                    console.log('Successfully logged in!');
                    setTimeout(() => {
                        document.getElementById('uploadSection').style.display = 'block';
                        document.getElementById('loginForm').style.display = 'none';
                        document.getElementById('loginMessage').style.display = 'none';
                    }, 500); // Redirect after 0.5 second
                }
            });
        },
        onFailure: function (err) {
            console.error('Error during login:', err);
            alert('Login failed!');
            document.getElementById('loginMessage').textContent = '';
        },
    });
});
