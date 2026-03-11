import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  ActivityIndicator, 
  Alert, 
  KeyboardAvoidingView, 
  Platform, 
  ScrollView 
} from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { COLORS } from '../constants/colors';
import { LOGIN_URL, REGISTER_URL } from '../constants/config';

/**
 * LoginScreen Component
 * Handles user authentication including login and registration flows.
 * Provides full cross-platform support (iOS, Android, Web).
 * Uses AsyncStorage for token persistence.
 *
 * @param {Object} props
 * @param {function(string): void} props.onLoginSuccess Callback invoked with token upon successful login
 */
export const LoginScreen = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between Login / Register
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState(''); 
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * Handle form submission for login or registration.
   * Performs validation, sends request to backend, and handles token storage.
   */
  const handleSubmit = async () => {
    // Basic input validation
    if (!username || !password || (!isLogin && !email)) {
      const msg = 'נא למלא את כל השדות הנדרשים';
      Platform.OS === 'web' ? alert(msg) : Alert.alert('שגיאה', msg);
      return;
    }

    setLoading(true);
    const url = isLogin ? LOGIN_URL : REGISTER_URL;

    const payload = isLogin 
      ? { username, password } 
      : { username, email, password };

    console.log(`Sending ${isLogin ? 'Login' : 'Register'} request to: ${url}`);

    try {
      const response = await axios.post(url, payload);
      console.log("Server Response:", response.data);

      if (isLogin) {
        // --- Login logic ---
        const token = response.data.access_token;
        if (token) {
          try {
            // Store token for cross-platform persistence
            await AsyncStorage.setItem('userToken', token);
            console.log("Token saved successfully to AsyncStorage");
          } catch (e) { 
            console.warn("AsyncStorage failed", e); 
          }
          onLoginSuccess(token);
        }
      } else {
        // --- Registration success flow ---
        const successMsg = 'החשבון נוצר בהצלחה! כעת ניתן להתחבר.';
        Platform.OS === 'web' ? alert(successMsg) : Alert.alert('הצלחה!', successMsg);

        // Reset form and switch to login screen
        setIsLogin(true);
        setPassword('');
        setEmail('');
      }
    } catch (error) {
      console.error("Auth Error:", error.response?.data || error.message);
      const errorMsg = error.response?.data?.error || error.response?.data?.message || 'אירעה שגיאה בחיבור לשרת';
      Platform.OS === 'web' ? alert(errorMsg) : Alert.alert(isLogin ? 'התחברות נכשלה' : 'הרשמה נכשלה', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.card}>
          <Text style={styles.title}>{isLogin ? 'ברוכים הבאים' : 'יצירת חשבון'}</Text>
          <Text style={styles.subtitle}>
            {isLogin ? 'התחבר כדי להמשיך ליומן שלך' : 'הצטרף אלינו והתחל לנהל יומן חכם'}
          </Text>

          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="שם משתמש"
              placeholderTextColor={COLORS.secondaryText}
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />

            {!isLogin && (
              <TextInput
                style={styles.input}
                placeholder="אימייל"
                placeholderTextColor={COLORS.secondaryText}
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
              />
            )}

            <TextInput
              style={styles.input}
              placeholder="סיסמה"
              placeholderTextColor={COLORS.secondaryText}
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
          </View>

          <TouchableOpacity 
            style={[styles.button, !isLogin && styles.registerButton]} 
            onPress={handleSubmit} 
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>{isLogin ? 'התחבר' : 'צור חשבון'}</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.switchContainer} 
            onPress={() => {
                setIsLogin(!isLogin);
                setEmail('');
                setPassword('');
            }}
          >
            <Text style={styles.switchText}>
              {isLogin ? 'אין לך חשבון? ' : 'כבר יש לך חשבון? '}
              <Text style={styles.switchAction}>{isLogin ? 'הרשם עכשיו' : 'התחבר כאן'}</Text>
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

// ---------------------------
// Styles
// ---------------------------
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  card: {
    backgroundColor: COLORS.leftBubble, 
    padding: 30,
    borderRadius: 20,
    elevation: 5,
    shadowColor: COLORS.background,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    maxWidth: 500,
    width: '100%',
    alignSelf: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: COLORS.text,
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: COLORS.secondaryText,
    textAlign: 'center',
    marginBottom: 30,
  },
  inputContainer: {
    marginBottom: 20,
  },
  input: {
    backgroundColor: COLORS.inputBackground,
    color: COLORS.text,
    borderRadius: 12,
    padding: 18,
    marginBottom: 15,
    textAlign: 'right',
    fontSize: 16,
  },
  button: {
    backgroundColor: COLORS.accent,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginTop: 10,
  },
  registerButton: {
    color: COLORS.secondaryText, 
  },
  buttonText: {
    color: COLORS.text,
    fontSize: 18,
    fontWeight: 'bold',
  },
  switchContainer: {
    marginTop: 25,
    alignItems: 'center',
  },
  switchText: {
    color: COLORS.secondaryText,
    fontSize: 14,
  },
  switchAction: {
    color: COLORS.accent,
    fontWeight: 'bold',
    textDecorationLine: 'underline',
  },
});