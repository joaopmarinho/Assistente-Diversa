import 'article_source.dart';

enum MessageRole { user, assistant }

class ChatMessage {
  const ChatMessage({
    required this.text,
    required this.role,
    this.sources = const [],
  });

  final String text;
  final MessageRole role;
  final List<ArticleSource> sources;
}
