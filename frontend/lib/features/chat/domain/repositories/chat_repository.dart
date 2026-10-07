import '../entities/article_source.dart';

class ChatReply {
  const ChatReply({required this.answer, required this.sources});

  final String answer;
  final List<ArticleSource> sources;
}

abstract interface class ChatRepository {
  Future<ChatReply> sendMessage({
    required String message,
    required String profile,
  });
}
