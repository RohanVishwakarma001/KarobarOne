"use client";
import React from "react";
import { Menu, X, Heart, ShoppingCart } from "lucide-react";
import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

export default function Header(): React.JSX.Element {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);
  const [wishlistOpen, setWishlistOpen] = useState<boolean>(false);
  const [cartOpen, setCartOpen] = useState<boolean>(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Excellence
            </div>
          </div>

          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="hover:text-blue-600 transition-colors">Home</a>
            <a href="#products" className="hover:text-blue-600 transition-colors">Products</a>
            
            <a href="#about" className="hover:text-blue-600 transition-colors">About</a>
            <a href="#usp" className="hover:text-blue-600 transition-colors">USP</a>
            <a href="#blog" className="hover:text-blue-600 transition-colors">Blogs</a>
            <a href="#contact" className="hover:text-blue-600 transition-colors">Contact</a>

            <div className="flex items-center gap-4">
              <button onClick={() => setWishlistOpen(!wishlistOpen)} className="relative hover:text-blue-600 transition-colors">
                <Heart size={24} />
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  0
                </span>
              </button>

              <button onClick={() => setCartOpen(!cartOpen)} className="relative hover:text-blue-600 transition-colors">
                <ShoppingCart size={24} />
                <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  0
                </span>
              </button>
            </div>
          </nav>

          <button className="md:hidden" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {menuOpen && (
          <nav className="md:hidden pb-4 flex flex-col space-y-4">
            <a href="#home" onClick={() => setMenuOpen(false)}>Home</a>
            <a href="#products" onClick={() => setMenuOpen(false)}>Products</a>
            <a href="#about" onClick={() => setMenuOpen(false)}>About</a>
            <a href="#usp" onClick={() => setMenuOpen(false)}>USP</a>
            <a href="#blog" onClick={() => setMenuOpen(false)}>Blog</a>
            <a href="#contact" onClick={() => setMenuOpen(false)}>Contact</a>

            <div className="flex items-center gap-4">
              <button onClick={() => setWishlistOpen(!wishlistOpen)} className="relative">
                <Heart size={24} />
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  0
                </span>
              </button>

              <button onClick={() => setCartOpen(!cartOpen)} className="relative">
                <ShoppingCart size={24} />
                <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  0
                </span>
              </button>
            </div>
          </nav>
        )}
      </div>

        <AnimatePresence>
  {(wishlistOpen || cartOpen) && (
    <>
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={() => {
          setWishlistOpen(false);
          setCartOpen(false);
        }}
        className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
      />

      {/* Wishlist Popup */}
      {wishlistOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -10, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          className="fixed top-20 right-4 md:right-8 w-80 md:w-96 bg-white rounded-xl shadow-2xl z-50 p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold">My Wishlist</h3>
            <button
              onClick={() => setWishlistOpen(false)}
              className="hover:bg-gray-100 p-1 rounded-full transition-colors"
            >
              <X size={20} />
            </button>
          </div>
          <div className="flex flex-col items-center justify-center py-12">
            <Heart size={64} className="text-gray-300 mb-4" />
            <p className="text-gray-500 mb-6">No items in wishlist</p>
            <button
              onClick={() => {
                setWishlistOpen(false);
                document.getElementById("products")?.scrollIntoView({ behavior: "smooth" });
              }}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-shadow"
            >
              Explore Products
            </button>
          </div>
        </motion.div>
      )}

      {/* Cart Popup */}
      {cartOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -10, scale: 0.95 }}
          transition={{ duration: 0.2 }}
          className="fixed top-20 right-4 md:right-8 w-80 md:w-96 bg-white rounded-xl shadow-2xl z-50 p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold">Your Cart</h3>
            <button
              onClick={() => setCartOpen(false)}
              className="hover:bg-gray-100 p-1 rounded-full transition-colors"
            >
              <X size={20} />
            </button>
          </div>
          <div className="flex flex-col items-center justify-center py-12">
            <ShoppingCart size={64} className="text-gray-300 mb-4" />
            <p className="text-gray-500 mb-6">Your cart is empty</p>
            <button
              onClick={() => {
                setCartOpen(false);
                document.getElementById("products")?.scrollIntoView({ behavior: "smooth" });
              }}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-shadow"
            >
              Continue Shopping
            </button>
          </div>
        </motion.div>
      )}
    </>
  )}
</AnimatePresence>

    </header>
  );
}