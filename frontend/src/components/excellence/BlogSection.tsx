"use client"
import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Calendar, User, X, ArrowRight } from 'lucide-react';

const blogPost = {
  image: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080',
  title: 'The Future of Digital Transformation in Modern Business',
  date: 'May 15, 2026',
  author: 'Sarah Johnson',
  summary: 'Discover how cutting-edge technology is reshaping the business landscape and what it means for your organization\'s growth strategy.',
  content: {
    intro: 'In today\'s rapidly evolving digital landscape, businesses face unprecedented opportunities and challenges. The convergence of artificial intelligence, cloud computing, and automation is fundamentally transforming how organizations operate and compete.',
    sections: [
      {
        heading: 'Understanding the Digital Revolution',
        text: 'Digital transformation is no longer optional—it\'s essential for survival in the modern marketplace. Companies that embrace technological innovation are experiencing 3-5x faster growth compared to their traditional competitors. This shift encompasses everything from customer experience to internal operations, creating new value streams and business models.'
      },
      {
        heading: 'Key Technologies Driving Change',
        text: 'Artificial Intelligence and Machine Learning are at the forefront of this revolution, enabling predictive analytics, personalized customer experiences, and automated decision-making. Cloud infrastructure provides the scalability needed to adapt quickly to market demands, while IoT devices generate valuable data insights that inform strategic decisions.'
      },
      {
        heading: 'The Human Element',
        text: 'Despite all the technological advancement, the human element remains crucial. Successful digital transformation requires a cultural shift within organizations. Employees must be empowered with new skills, and leadership must champion innovation while maintaining focus on customer value and business outcomes.'
      },
      {
        heading: 'Implementation Strategy',
        text: 'Start with a clear vision aligned with business objectives. Prioritize initiatives that deliver quick wins while building toward long-term transformation. Invest in scalable infrastructure, foster a culture of continuous learning, and maintain customer-centricity throughout the journey. Remember that transformation is a marathon, not a sprint.'
      },
      {
        heading: 'Measuring Success',
        text: 'Define clear KPIs that go beyond technology metrics. Track customer satisfaction, operational efficiency, employee engagement, and revenue growth. Regular assessment and iteration ensure your transformation efforts remain aligned with evolving business needs and market conditions.'
      }
    ],
    conclusion: 'The future belongs to organizations that can adapt, innovate, and leverage technology to create exceptional value. By embracing digital transformation with a strategic, human-centered approach, businesses can position themselves for sustainable success in an increasingly digital world.'
  }
};

export default function BlogSection() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-5xl text-center mb-16">Featured Article</h2>

          <div
            onClick={() => setIsModalOpen(true)}
            className="grid grid-cols-1 lg:grid-cols-2 gap-8 bg-white rounded-2xl shadow-xl overflow-hidden cursor-pointer hover:shadow-2xl transition-shadow"
          >
            <div className="h-full">
              <img
                src={blogPost.image}
                alt={blogPost.title}
                className="w-full h-full object-cover min-h-[300px] lg:min-h-[400px]"
              />
            </div>

            <div className="p-8 lg:p-12 flex flex-col justify-center">
              <div className="flex gap-4 mb-4 text-gray-600">
                <div className="flex items-center gap-2">
                  <Calendar size={18} />
                  <span>{blogPost.date}</span>
                </div>
                <div className="flex items-center gap-2">
                  <User size={18} />
                  <span>{blogPost.author}</span>
                </div>
              </div>

              <h3 className="text-3xl lg:text-4xl mb-4">{blogPost.title}</h3>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                {blogPost.summary}
              </p>

              <button className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-shadow self-start">
                Read More
                <ArrowRight size={20} />
              </button>
            </div>
          </div>
        </div>
      </section>

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
              className="fixed inset-4 md:inset-8 lg:inset-16 bg-white rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col"
            >
              <button
                onClick={() => setIsModalOpen(false)}
                className="absolute top-4 right-4 z-10 bg-white/90 backdrop-blur-sm hover:bg-white p-2 rounded-full shadow-lg transition-colors"
              >
                <X size={24} />
              </button>

              <div className="overflow-y-auto flex-1">
                <img
                  src={blogPost.image}
                  alt={blogPost.title}
                  className="w-full h-64 md:h-80 lg:h-96 object-cover"
                />

                <div className="max-w-4xl mx-auto px-6 md:px-12 py-12">
                  <h1 className="text-3xl md:text-4xl lg:text-5xl mb-6">
                    {blogPost.title}
                  </h1>

                  <div className="flex flex-wrap gap-6 mb-8 text-gray-600 pb-6 border-b border-gray-200">
                    <div className="flex items-center gap-2">
                      <User size={20} />
                      <span className="text-lg">{blogPost.author}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar size={20} />
                      <span className="text-lg">{blogPost.date}</span>
                    </div>
                  </div>

                  <div className="prose prose-lg max-w-none">
                    <p className="text-xl leading-relaxed mb-8 text-gray-700">
                      {blogPost.content.intro}
                    </p>

                    {blogPost.content.sections.map((section, idx) => (
                      <div key={idx} className="mb-8">
                        <h2 className="text-2xl md:text-3xl mb-4">
                          {section.heading}
                        </h2>
                        <p className="text-lg leading-relaxed text-gray-700">
                          {section.text}
                        </p>
                      </div>
                    ))}

                    <div className="mt-12 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border-l-4 border-blue-600">
                      <p className="text-lg leading-relaxed text-gray-800">
                        <strong>Conclusion:</strong> {blogPost.content.conclusion}
                      </p>
                    </div>
                  </div>

                  <div className="mt-12 pt-8 border-t border-gray-200">
                    <button
                      onClick={() => setIsModalOpen(false)}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg hover:shadow-lg transition-shadow"
                    >
                      Close Article
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
