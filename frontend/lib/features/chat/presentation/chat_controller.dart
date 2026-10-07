import 'package:flutter/foundation.dart';

import '../domain/entities/chat_message.dart';
import '../domain/use_cases/send_message.dart';

class ChatController extends ChangeNotifier {
  ChatController(this._sendMessage);

  final SendMessage _sendMessage;
  final List<ChatMessage> _messages = [];
  String _profile = 'professor';
  bool _isSending = false;
  String? _error;

  List<ChatMessage> get messages => List.unmodifiable(_messages);
  String get profile => _profile;
  bool get isSending => _isSending;
  String? get error => _error;

  void selectProfile(String profile) {
    _profile = profile;
    notifyListeners();
  }

  Future<void> send(String text) async {
    final message = text.trim();
    if (message.isEmpty || _isSending) return;

    _messages.add(ChatMessage(text: message, role: MessageRole.user));
    _isSending = true;
    _error = null;
    notifyListeners();

    try {
      final reply = await _sendMessage(message: message, profile: _profile);
      _messages.add(
        ChatMessage(
          text: reply.answer,
          role: MessageRole.assistant,
          sources: reply.sources,
        ),
      );
    } catch (_) {
      _error = 'Não foi possível conectar à API. Verifique se o backend está ativo.';
    } finally {
      _isSending = false;
      notifyListeners();
    }
  }
}
