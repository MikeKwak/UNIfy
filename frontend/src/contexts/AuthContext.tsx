import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  signIn, 
  signUp, 
  signOut, 
  getCurrentUser, 
  confirmSignUp, 
  resendSignUpCode, 
  resetPassword, type ResetPasswordOutput, 
  confirmResetPassword, type ConfirmResetPasswordInput
} from 'aws-amplify/auth';
import { Hub } from 'aws-amplify/utils';

interface User {
  userId: string;
  username: string;
  email?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signOut: () => Promise<void>;
  confirmSignUp: (email: string, code: string) => Promise<void>;
  resendSignUpCode: (email: string) => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  confirmResetPassword: (username: string, confirmationCode: string, newPassword: string) => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkUser();
    
    // Listen for auth events
    const unsubscribe = Hub.listen('auth', ({ payload }) => {
      switch (payload.event) {
        case 'signedIn':
          checkUser();
          break;
        case 'signedOut':
          setUser(null);
          break;
        case 'tokenRefresh':
          checkUser();
          break;
      }
    });

    return unsubscribe;
  }, []);

  const checkUser = async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser({
        userId: currentUser.userId,
        username: currentUser.username,
        email: currentUser.signInDetails?.loginId,
      });
    } catch (error) {
      console.log('No authenticated user');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (email: string, password: string) => {
    try {
      await signIn({
        username: email,
        password,
      });
      // User state will be updated via Hub listener
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const handleSignUp = async (email: string, password: string, name: string) => {
    try {
      await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            email,
            name,
          },
        },
      });
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      // User state will be updated via Hub listener
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  };

  const handleConfirmSignUp = async (email: string, code: string) => {
    try {
      await confirmSignUp({
        username: email,
        confirmationCode: code,
      });
    } catch (error) {
      console.error('Confirm sign up error:', error);
      throw error;
    }
  };

  const handleResendSignUpCode = async (email: string) => {
    try {
      await resendSignUpCode({
        username: email,
      });
    } catch (error) {
      console.error('Resend sign up code error:', error);
      throw error;
    }
  };
  
  const handleResetPassword = async (username: string): Promise<void> => {
    try {
      const output = await resetPassword({ username });
      handleResetPasswordNextSteps(output);
    } catch (error) {
      console.error('Reset password error:', error);
      throw error;
    }
  };

  function handleResetPasswordNextSteps(output: ResetPasswordOutput) {
  const { nextStep } = output;
  switch (nextStep.resetPasswordStep) {
    case 'CONFIRM_RESET_PASSWORD_WITH_CODE':
      const codeDeliveryDetails = nextStep.codeDeliveryDetails;
      console.log(
        `Confirmation code was sent to ${codeDeliveryDetails.deliveryMedium}`
      );
      // Collect the confirmation code from the user and pass to confirmResetPassword.
      break;
    case 'DONE':
      console.log('Successfully reset password.');
      break;
  }
}

const handleConfirmResetPassword = async (username: string, confirmationCode: string, newPassword: string): Promise<void> => {
  try {
    const input: ConfirmResetPasswordInput = {
      username,
      confirmationCode,
      newPassword,
    };
    const output = await confirmResetPassword(input);
    console.log('Password reset confirmed:', output);
  } catch (error) {
    console.error('Confirm reset password error:', error);
    throw error;
  }
}

  const value: AuthContextType = {
    user,
    loading,
    signIn: handleSignIn,
    signUp: handleSignUp,
    signOut: handleSignOut,
    confirmSignUp: handleConfirmSignUp,
    resendSignUpCode: handleResendSignUpCode,
    resetPassword: handleResetPassword,
    confirmResetPassword: handleConfirmResetPassword,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
