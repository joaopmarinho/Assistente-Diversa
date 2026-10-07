import 'package:flutter/material.dart';

import 'core/network/api_client.dart';
import 'features/chat/data/datasources/chat_remote_data_source.dart';
import 'features/chat/data/repositories/chat_repository_impl.dart';
import 'features/chat/domain/use_cases/send_message.dart';
import 'features/chat/presentation/chat_controller.dart';
import 'features/chat/presentation/chat_page.dart';

void main() {
  final apiClient = ApiClient();
  final repository = ChatRepositoryImpl(
    ChatRemoteDataSource(apiClient),
  );
  final controller = ChatController(SendMessage(repository));

  runApp(AssistenteDiversaApp(controller: controller));
}

class AssistenteDiversaApp extends StatelessWidget {
  const AssistenteDiversaApp({required this.controller, super.key});

  final ChatController controller;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Assistente Diversa',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF176B62)),
        useMaterial3: true,
      ),
      home: ChatPage(controller: controller),
    );
  }
}
