class Post {
  final String productName;

  Post(this.productName);


  factory Post.fromJson(Map<String, dynamic> json) {
  return Post(json['items']['0']['product_name']);
  }  
}
