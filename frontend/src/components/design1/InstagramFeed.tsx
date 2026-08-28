import {  FaInstagram } from "react-icons/fa";

const instagramPosts = [
  {
    image: 'https://images.unsplash.com/photo-1758691737543-09a1b2b715fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '1.2k',
    caption: 'Team collaboration at its finest'
  },
  {
    image: 'https://images.unsplash.com/photo-1758518731457-5ef826b75b3b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '890',
    caption: 'Innovation meets execution'
  },
  {
    image: 'https://images.unsplash.com/photo-1647427060118-4911c9821b82?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '2.1k',
    caption: 'Behind the scenes at our facility'
  },
  {
    image: 'https://images.unsplash.com/photo-1717386255773-1e3037c81788?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '1.5k',
    caption: 'Quality in every detail'
  },
  {
    image: 'https://images.unsplash.com/photo-1674981208693-de5a9c4c4f44?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '980',
    caption: 'Building tomorrow, today'
  },
  {
    image: 'https://images.unsplash.com/photo-1662318682624-89652a1c8206?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=400',
    likes: '1.8k',
    caption: 'Excellence is our standard'
  }
];

export default function InstagramFeed() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-center gap-3 mb-4">
          <FaInstagram className="w-8 h-8 text-pink-600" />
          <h2 className="text-4xl md:text-5xl text-center">
            Follow Us on Instagram
          </h2>
        </div>
        <p className="text-center text-gray-600 mb-12 text-lg">
          Stay updated with our latest projects and updates
        </p>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {instagramPosts.map((post, index) => (
            <div
              key={index}
              className="group relative aspect-square rounded-lg overflow-hidden cursor-pointer shadow-lg hover:shadow-2xl transition-all duration-300"
            >
              <img
                src={post.image}
                alt={post.caption}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/0 to-black/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                <p className="text-white text-sm mb-2">{post.caption}</p>
                <p className="text-white/80 text-xs">❤️ {post.likes}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-8">
          <a
            href="https://instagram.com/yourcompany"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-3 rounded-full transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            <FaInstagram className="w-5 h-5" />
            Follow @yourcompany
          </a>
        </div>
      </div>
    </section>
  );
}
