import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/post.dart';
import 'dart:async';
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme:
            ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 0, 0, 0)),
        useMaterial3: true,
      ),
      home: const Home(),
    );
  }
}

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  Future<Post?>? post;

  void clickGetButton() {
    setState(() {
      post = fetchPost();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: const Text("Snack Finder"),
        ),
        body: SizedBox(
            height: 500,
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                FutureBuilder<Post?>(
                  future: post,
                  builder: (context, snapshot) {
                    // print(snapshot);
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const CircularProgressIndicator();
                    } else if (snapshot.connectionState ==
                        ConnectionState.none) {
                      return Container();
                    } else if (snapshot.hasData) {
                      return buildDataWidget(context, snapshot);
                    } else if (snapshot.hasError) {
                      return Text("${snapshot.error}");
                    } else {
                      return Container();
                    }
                  },
                ),
                SizedBox(
                    width: 200,
                    child: ElevatedButton(
                      onPressed: () => clickGetButton(),
                      child: const Text("GET"),
                    ))
              ],
            )));
  }
}

// GET Api Request
Future<Post> fetchPost() async {
  final uri = Uri.parse("http://127.0.0.1:8000/");
  final response = await http.get(uri);

  if (response.statusCode == 200) {
    return Post.fromJson(json.decode(response.body));
  } else {
    throw Exception("Failed to load post");
  }
}

Widget buildDataWidget(context, snapshot) => Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.all(15.0),
            child: Text(snapshot.data.productName),
          )
        ]);
