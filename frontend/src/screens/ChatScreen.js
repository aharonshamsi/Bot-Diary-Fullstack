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
import { startRecording, stopRecordingAndTranscribe } from '../services/audioService';

export const ChatScreen = ({ userToken, onLogout }) => {

  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

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

  const handleStartRecording = async () => {
    setIsRecording(true);
    await startRecording();
  };

  const handleStopRecording = async () => {
  setIsRecording(false);
  setIsTyping(true);

  try {

    const text = await stopRecordingAndTranscribe();

    if (text) {
      onSend([{
        _id: Math.random().toString(),
        text,
        createdAt: new Date(),
        user: { _id: 1 }
      }]);
    }

  } catch (err) {
    console.error("Transcription error:", err);
    setIsTyping(false);
  }
};

  const onSend = useCallback(async (newMessages = []) => {

    setMessages(previous => GiftedChat.append(previous, newMessages));
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

      setMessages(previous => GiftedChat.append(previous, [botMsg]));

    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setIsTyping(false);
    }

  }, [userToken]);

  const renderInputToolbarStable = useCallback((props) => {
    return renderInputToolbar(props, handleStartRecording, handleStopRecording, isRecording);
  }, [isRecording]);

  return (
    <SafeAreaView style={styles.container}>

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
          renderInputToolbar={renderInputToolbarStable}
          renderSend={renderSend}
          renderFooter={() => renderFooter(isTyping)}

          isTyping={isTyping}
          scrollToBottom

          timeTextStyle={{
            left: { color: COLORS.secondaryText },
            right: { color: COLORS.secondaryText }
          }}

          listViewProps={{
            style: { backgroundColor: COLORS.background }
          }}
        />

      </View>

      {Platform.OS === 'android' && (
        <KeyboardAvoidingView behavior="padding" />
      )}

    </SafeAreaView>
  );
};

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: COLORS.background
  },

  innerContainer: {
    flex: 1,
    width: '100%',
    maxWidth: Platform.OS === 'web' ? 600 : '100%',
    alignSelf: 'center'
  }

});