"use client";
import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { ShoppingCart, Heart, X } from 'lucide-react';

interface FlipCardProps {
  title: string;
  description: string;
  image: string;
  backContent: string;
  longDescription: string;
  onAddToCart: () => void;
  onAddToWishlist: () => void;
}

export default function FlipCard({
  title,
  description,
  image,
  backContent,
  longDescription,
  onAddToCart,
  onAddToWishlist
}: FlipCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleCardClick = (e: React.MouseEvent) => {
    const target = e.target as HTMLElement;
    if (!target.closest('button')) {
      setIsModalOpen(true);
    }
  };

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToCart();
  };

  const handleAddToWishlist = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToWishlist();
  };

  return (
    <>
      <div
        className="h-96 cursor-pointer perspective-1000"
        onMouseEnter={() => setIsFlipped(true)}
        onMouseLeave={() => setIsFlipped(false)}
        onClick={handleCardClick}
      >
        <motion.div
          className="relative w-full h-full"
          initial={false}
          animate={{ rotateY: isFlipped ? 180 : 0 }}
          transition={{ duration: 0.6 }}
          style={{ transformStyle: 'preserve-3d' }}
        >
          {/* Front Side */}
          <div
            className="absolute inset-0 bg-white rounded-xl shadow-lg overflow-hidden flex flex-col"
            style={{ backfaceVisibility: 'hidden' }}
          >
            <div className="h-48 overflow-hidden">
              <img
                src={image}
                alt={title}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 p-6 flex flex-col">
              <h3 className="text-2xl text-center mb-auto">{title}</h3>

              <div className="flex gap-3 mt-4">
                <button
                  onClick={handleAddToCart}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 rounded-lg hover:shadow-lg transition-shadow flex items-center justify-center gap-2"
                >
                  <ShoppingCart size={18} />
                  Add to Cart
                </button>
                <button
                  onClick={handleAddToWishlist}
                  className="flex-1 border-2 border-blue-600 text-blue-600 py-2 px-4 rounded-lg hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
                >
                  <Heart size={18} />
                  Wishlist
                </button>
              </div>
            </div>
          </div>

          {/* Back Side */}
          <div
            className="absolute inset-0 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl shadow-lg p-8 flex flex-col justify-between text-white"
            style={{
              backfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)'
            }}
          >
            <div className="flex-1 flex items-center justify-center text-center">
              <p className="text-lg">{backContent}</p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleAddToCart}
                className="flex-1 bg-white text-blue-600 py-2 px-4 rounded-lg hover:bg-gray-100 transition-colors flex items-center justify-center gap-2"
              >
                <ShoppingCart size={18} />
                Add to Cart
              </button>
              <button
                onClick={handleAddToWishlist}
                className="flex-1 border-2 border-white text-white py-2 px-4 rounded-lg hover:bg-white/10 transition-colors flex items-center justify-center gap-2"
              >
                <Heart size={18} />
                Wishlist
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
            />

            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 50, scale: 0.95 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="fixed inset-4 md:inset-12 lg:inset-24 bg-white rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col max-w-4xl mx-auto"
            >
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute top-4 right-4 z-10 bg-white/90 backdrop-blur-sm hover:bg-white p-2 rounded-full shadow-lg transition-colors"
              >
                <X size={24} />
              </button>

              <div className="overflow-y-auto flex-1 p-8 md:p-12">
                <h2 className="text-3xl md:text-4xl text-center mb-8">{title}</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                  <div>
                    <img
                      src={image}
                      alt={title}
                      className="w-full h-64 md:h-80 object-cover rounded-xl shadow-lg"
                    />
                  </div>

                  <div className="flex flex-col justify-center">
                    <h3 className="text-xl mb-4">Description</h3>
                    <p className="text-gray-700 leading-relaxed">{description}</p>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-8">
                  <h3 className="text-2xl text-center mb-6">Details</h3>
                  <p className="text-lg text-gray-700 leading-relaxed text-center max-w-3xl mx-auto">
                    {longDescription}
                  </p>
                </div>

                <div className="flex gap-4 mt-8 justify-center">
                  <button
                    onClick={(e) => {
                      handleAddToCart(e);
                      setIsModalOpen(false);
                    }}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-8 rounded-lg hover:shadow-lg transition-shadow flex items-center gap-2"
                  >
                    <ShoppingCart size={20} />
                    Add to Cart
                  </button>
                  <button
                    onClick={(e) => {
                      handleAddToWishlist(e);
                      setIsModalOpen(false);
                    }}
                    className="border-2 border-blue-600 text-blue-600 py-3 px-8 rounded-lg hover:bg-blue-50 transition-colors flex items-center gap-2"
                  >
                    <Heart size={20} />
                    Add to Wishlist
                  </button>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
