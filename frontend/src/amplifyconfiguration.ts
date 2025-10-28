import { Amplify } from 'aws-amplify';

// Get environment variables
const userPoolId = import.meta.env.VITE_AWS_USER_POOL_ID;
const userPoolClientId = import.meta.env.VITE_AWS_USER_POOL_CLIENT_ID;
const region = import.meta.env.VITE_AWS_REGION;

// Validate required environment variables
if (!userPoolId) {
  throw new Error('VITE_AWS_USER_POOL_ID environment variable is required');
}
if (!userPoolClientId) {
  throw new Error('VITE_AWS_USER_POOL_CLIENT_ID environment variable is required');
}
if (!region) {
  throw new Error('VITE_AWS_REGION environment variable is required');
}

const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: userPoolId,
      userPoolClientId: userPoolClientId,
      region: region,
      loginWith: {
        email: true,
        username: false,
        phone: false,
      },
      signUpVerificationMethod: 'code',
    }
  }
};

export const configureAmplify = () => {
  Amplify.configure(amplifyConfig);
};

export default amplifyConfig;
