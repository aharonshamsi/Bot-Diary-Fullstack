import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity, Platform } from 'react-native';
import { Bubble, MessageText, InputToolbar, Send } from 'react-native-gifted-chat';
import { MaterialIcons } from '@expo/vector-icons';
import { COLORS } from '../constants/colors';

// Avatar
export const renderAvatar = () => (
  <View style={styles.avatarCircle}>
    <Text style={styles.avatarText}>EA</Text>
  </View>
);

// Bubble
export const renderBubble = (props) => (
  <Bubble
    {...props}
    wrapperStyle={{
      left: styles.bubbleLeft,
      right: styles.bubbleRight,
    }}
    containerStyle={{
      left: { marginLeft: 5, flexShrink: 1 },
      right: { marginRight: 5, flexShrink: 1 },
    }}
    textStyle={{
      left: styles.bubbleText,
      right: styles.bubbleText,
    }}
  />
);

// Message text
export const renderMessageText = (props) => (
  <MessageText
    {...props}
    textStyle={{
      left: styles.messageText,
      right: styles.messageText,
    }}
  />
);

// Mic button
export const renderActions = (onPressIn, onPressOut, isRecording) => (
  <TouchableOpacity
    onPress={Platform.OS === 'web' ? (isRecording ? onPressOut : onPressIn) : undefined}
    onPressIn={Platform.OS !== 'web' ? onPressIn : undefined}
    onPressOut={Platform.OS !== 'web' ? onPressOut : undefined}
    style={styles.micButton}
    activeOpacity={0.7}
  >
    <MaterialIcons
      name={isRecording ? "stop-circle" : "mic"}
      size={28}
      color={isRecording ? '#FF3B30' : COLORS.accent}
    />
  </TouchableOpacity>
);

// Input toolbar
export const renderInputToolbar = (props, onPressIn, onPressOut, isRecording) => (
  <InputToolbar
    {...props}
    containerStyle={styles.inputToolbar}
    renderActions={() => renderActions(onPressIn, onPressOut, isRecording)}
  />
);

// Send button
export const renderSend = (props) => (
  <Send {...props} containerStyle={styles.sendButton}>
    <MaterialIcons name="send" size={24} color={COLORS.accent} />
  </Send>
);

// Typing indicator
export const renderFooter = (isTyping) => {

  if (!isTyping) return null;

  return (
    <View style={styles.typingContainer}>
      <Text style={styles.typingText}>מעבד נתונים</Text>
      <ActivityIndicator
        size="small"
        color={COLORS.accent}
        style={{ marginLeft: 8 }}
      />
    </View>
  );
};

const styles = StyleSheet.create({

  avatarCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: COLORS.avatarBackground,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.avatarText,
  },

  avatarText: {
    color: COLORS.avatarText,
    fontSize: 12,
    fontWeight: 'bold',
  },

  bubbleLeft: {
    backgroundColor: COLORS.leftBubble,
    borderRadius: 15,
    marginBottom: 5,
    maxWidth: '80%',
    paddingVertical: 6,
    paddingHorizontal: 4,
  },

  bubbleRight: {
    backgroundColor: COLORS.rightBubble,
    borderRadius: 15,
    marginBottom: 5,
    minWidth: 40,
    alignSelf: 'flex-end',
    marginLeft: 50,
  },

  bubbleText: {
    color: COLORS.text,
    fontSize: 16,
  },

  messageText: {
    textAlign: 'right',
    writingDirection: 'rtl',
    lineHeight: 22,
    color: '#ffffff',
    paddingHorizontal: 10,
    flexShrink: 1,
    flexWrap: 'wrap',
  },

  inputToolbar: {
    backgroundColor: COLORS.inputBackground,
    borderTopWidth: 0,
    marginHorizontal: 10,
    marginBottom: 5,
    borderRadius: 25,
    paddingHorizontal: 5,
  },

  sendButton: {
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
    marginBottom: 5,
  },

  micButton: {
    marginLeft: 10,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 5,
    minWidth: 40,
  },

  typingContainer: {
    paddingLeft: 20,
    paddingVertical: 5,
    flexDirection: 'row-reverse',
    alignItems: 'center',
  },

  typingText: {
    fontSize: 12,
    color: COLORS.secondaryText,
    fontStyle: 'italic',
  },

});