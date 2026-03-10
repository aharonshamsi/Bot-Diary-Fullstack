// =========================================================
// ChatScreen
// =========================================================
// Main chat interface using GiftedChat. Handles:
// 1. Displaying initial system message.
// 2. Sending user messages to the bot API.
// 3. Rendering custom UI components (bubbles, avatar, input, send button, footer).
// 4. Typing indicator management.
// =========================================================

import React, { useState, useCallback, useEffect } from 'react';
import { StyleSheet, View, SafeAreaView, Platform, KeyboardAvoidingView } from 'react-native';
import { GiftedChat } from 'react-native-gifted-chat';

import { COLORS } from '../constants/colors';
import { sendMessageToBot } from '../services/botApi';
import { Header } from '../components/Header';
import { 
  renderAvatar, 
  renderBubble, 
  renderMessageText, 
  renderInputToolbar, 
  renderSend, 
  renderFooter 
} from '../components/ChatCustomUI';

import 'react-native-get-random-values';

export const ChatScreen = ({ userToken, onLogout }) => {
  // ---------------------------
  // State
  // ---------------------------
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  // ---------------------------
  // Initial system message
  // ---------------------------
  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: 'שלום! המערכת מחוברת. איך אפשר לעזור היום?',
        createdAt: new Date(),
        user: { _id: 2, name: 'Smart Agent' },
      },
    ]);
  }, []);

  // ---------------------------
  // Handle sending messages
  // ---------------------------
  const onSend = useCallback(async (newMessages = []) => {
    setMessages(prev => GiftedChat.append(prev, newMessages));
    const userText = newMessages[0].text;

    setIsTyping(true);

    try {
      const response = await sendMessageToBot(userText, userToken);

      const botMsg = {
        _id: Math.random().toString(),
        text: response.reply,
        createdAt: new Date(),
        user: { _id: 2, name: 'Smart Agent' },
      };

      setMessages(prev => GiftedChat.append(prev, [botMsg]));
    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setIsTyping(false);
    }
  }, [userToken]);

  // ---------------------------
  // Render
  // ---------------------------
  return (
    <SafeAreaView style={styles.container}>
      {/* Header with logout */}
      <Header title="Agent Desk" onLogout={onLogout} />

      <View style={styles.innerContainer}>
        <GiftedChat
          messages={messages}
          onSend={msgs => onSend(msgs)}
          user={{ _id: 1 }}
          placeholder="הקלד הודעה..."
          locale="he"
          renderAvatar={renderAvatar}
          renderBubble={renderBubble}
          renderMessageText={renderMessageText}
          renderInputToolbar={renderInputToolbar}
          renderSend={renderSend}
          renderFooter={() => renderFooter(isTyping)}
          isTyping={isTyping}
          alwaysShowSend
          scrollToBottom
          timeTextStyle={{ 
            left: { color: COLORS.secondaryText }, 
            right: { color: COLORS.secondaryText } 
          }}
          listViewProps={{
            style: { backgroundColor: COLORS.background },
          }}
        />
      </View>

      {/* Android Keyboard handling */}
      {Platform.OS === 'android' && <KeyboardAvoidingView behavior="padding" />}
    </SafeAreaView>
  );
};

// ---------------------------
// Styles
// ---------------------------
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  innerContainer: {
    flex: 1,
    width: '100%',
    maxWidth: Platform.OS === 'web' ? 600 : '100%',
    alignSelf: 'center',
  },
});