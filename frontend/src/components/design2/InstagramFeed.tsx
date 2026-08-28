import { FaInstagram } from "react-icons/fa";

const instagramImages = [
  'https://images.unsplash.com/photo-1728836882608-6911cc2d6fb6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1728836883112-65f57b5f6d52?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1689525970033-948720b0ccf8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1669723009423-6c1b3d11dd92?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1623932078828-c768e94bc64b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1516798705208-066b05ced1cd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1770048532658-14834b7acef8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1648912869366-b89a51f52d44?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80',
  'https://images.unsplash.com/photo-1648912916310-d398d7eb5336?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600&q=80'
];

export default function InstagramFeed() {
  return (
    <section className="py-20 px-4 bg-gray-50 overflow-hidden">
      <div className="container mx-auto">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <FaInstagram className="text-pink-600" size={40} />
            <h2 className="text-4xl md:text-5xl">Follow Our Journey</h2>
          </div>
          <p className="text-gray-600 text-lg">
            @corporatepro on Instagram
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
          {instagramImages.map((image, index) => (
            <div
              key={index}
              className="aspect-square overflow-hidden rounded-lg group cursor-pointer relative"
            >
              <img
                src={image}
                alt={`Instagram post ${index + 1}`}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-pink-600/0 group-hover:bg-pink-600/20 transition-colors" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
