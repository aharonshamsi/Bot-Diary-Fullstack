import { Audio } from 'expo-av';
import axios from 'axios';
import { Config } from '../constants/config';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native'; 

// Global recording object
let recording = null;

/**
 * Request microphone permissions from the user.
 * @returns {Promise<boolean>} True if granted, false otherwise
 */
export const getPermissions = async () => {
  try {
    const { status } = await Audio.requestPermissionsAsync();
    return status === 'granted';
  } catch (err) {
    console.error('Error getting microphone permissions', err);
    return false;
  }
};

/**
 * Start audio recording.
 * Configures audio mode depending on platform to ensure proper recording.
 * Cleans up any previous recording to prevent memory leaks.
 * @returns {Promise<Audio.Recording|null>} Recording object or null on failure
 */
export const startRecording = async () => {
  try {
    const hasPermission = await getPermissions();
    if (!hasPermission) {
      console.warn('No microphone permission');
      return null;
    }

    // Audio configuration for iOS and Android
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
      shouldDuckAndroid: true,
      playThroughEarpieceAndroid: false,
      staysActiveInBackground: false,
    });

    // Clean up previous recording to prevent memory leaks
    if (recording !== null) {
      await recording.stopAndUnloadAsync();
      recording = null;
    }

    const { recording: newRecording } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    
    recording = newRecording;
    console.log('Recording started');
    return recording;

  } catch (err) {
    console.error('Failed to start recording', err);
    recording = null;
    return null;
  }
};

/**
 * Stop the current recording and transcribe it via backend API.
 * @returns {Promise<string|null>} Transcribed text or null on failure
 */
export const stopRecordingAndTranscribe = async () => {
  try {
    if (!recording) {
      console.log('No recording object found to stop');
      return null;
    }

    console.log('Stopping recording...');
    
    // Stop and unload recording from memory
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI(); 
    
    // Reset recording object to allow new recordings
    recording = null;

    if (!uri) {
      console.error('No URI found for the recording');
      return null;
    }

    // Send audio file to backend for transcription
    return await uploadAudio(uri);

  } catch (err) {
    console.error('Failed to stop recording', err);
    recording = null; // Ensure cleanup on error
    return null;
  }
};

/**
 * Upload audio file to Flask backend transcription endpoint.
 * Handles platform-specific URI adjustments for Web, iOS, and Android.
 * Includes Authorization header from AsyncStorage token.
 * @param {string} uri - URI of the audio file
 * @returns {Promise<string|null>} Transcribed text or null on error
 */
const uploadAudio = async (uri) => {
  try {
    const token = await AsyncStorage.getItem('userToken');
    
    // Critical check: ensure token exists and is valid
    if (!token || token === 'undefined' || token === 'null') {
      console.error("AudioService: Valid token is missing. Please re-login.");
      return null;
    }

    const formData = new FormData();
    
    if (Platform.OS === 'web') {
      // Web: fetch blob from URI
      const response = await fetch(uri);
      const blob = await response.blob();
      formData.append('file', blob, 'recording.m4a');
    } else {
      // Mobile: send file object with correct URI and type
      formData.append('file', {
        uri: Platform.OS === 'ios' ? uri.replace('file://', '') : uri,
        type: 'audio/m4a',
        name: 'recording.m4a',
      });
    }

    const response = await axios.post(`${Config.BASE_URL}/transcribe`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        // Note: On Web, do not manually set Content-Type for FormData
      },
    });

    return response.data.text;

  } catch (err) {
    console.error('Upload error status:', err.response?.status);
    console.error('Upload error data:', err.response?.data);
    return null;
  }
};