import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useLocation } from '@docusaurus/router';

const BACKEND_URL = 'http://localhost:8000'; // Replace with your backend URL in production

const BookContent = () => {
  const [bookContent, setBookContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('en'); // Default to English
  const [error, setError] = useState('');

  const location = useLocation();

  // Function to fetch book content based on language
  useEffect(() => {
    fetchBookContent();
  }, [language]);

  const fetchBookContent = async () => {
    setIsLoading(true);
    setError('');

    try {
      // First try to get the documents
      const response = await fetch(`${BACKEND_URL}/docs`);
      const data = await response.json();

      if (data && data.length > 0) {
        // Use the content from the first document
        let content = data[0].title || data[0].content || 'Book content will appear here';

        // If language is Urdu, translate the content
        if (language === 'ur') {
          const translationResponse = await fetch(`${BACKEND_URL}/translate`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              text: content,
              source_lang: 'en',
              target_lang: 'ur'
            })
          });

          const translationData = await translationResponse.json();
          content = translationData.translated_text || content;
        }

        setBookContent(content);
      } else {
        // If no documents found, provide sample content in English
        const englishContent = `# Physical AI & Humanoid Robotics: Bridging the Digital Brain and the Physical Body

## Chapter 1: Introduction to Physical AI

Physical AI represents a paradigm shift in artificial intelligence, where cognitive systems are embodied in physical forms that interact with the real world. This field combines machine learning, robotics, and embodied cognition to create systems that learn through physical interaction.

## Chapter 2: Humanoid Robotics Design

Humanoid robots are designed to mimic human form and behavior. Key components include:

- **Actuators**: Motor systems that enable movement
- **Sensors**: Cameras, microphones, and tactile sensors for perception
- **Control Systems**: Algorithms that coordinate movement and behavior
- **Learning Systems**: AI that adapts based on experience

## Chapter 3: Control Systems for Physical Agents

Effective control of physical systems requires sophisticated algorithms that can handle real-time constraints, uncertainty, and dynamic environments. Modern approaches combine classical control theory with machine learning.

## Chapter 4: Sensor Integration and Perception

Robots must interpret complex sensory data to understand their environment. This involves computer vision, audio processing, and multi-sensor fusion techniques.

## Chapter 5: Motion Planning and Control

Planning complex movements in dynamic environments requires sophisticated algorithms that can reason about physics, obstacles, and goals in real-time.

## Chapter 6: Learning in Physical Systems

Physical AI systems learn through interaction with their environment, building models of physics, affordances, and causal relationships through experience.

## Chapter 7: Applications and Future Directions

Physical AI has applications in manufacturing, healthcare, assistive technology, and exploration. The future promises increasingly capable and autonomous embodied systems.`;

        if (language === 'ur') {
          // Provide translated content for Urdu
          setBookContent(`# فزیکل ای آئی اور ہیومنوائڈ روبوٹکس: ڈیجیٹل دماغ اور جسمانی سریلے کو ملانا

## باب 1: فزیکل ای آئی کا تعارف

فزیکل ای آئی مصنوعی ذہانت میں ایک نظریاتی بدلاؤ کی نمائندگی کرتا ہے، جہاں ذہین نظام جسمانی اشکال میں جاری کیے جاتے ہیں جو حقیقی دنیا کے ساتھ تعامل کرتے ہیں۔ یہ مشین لرننگ، روبوٹکس، اور جسمانی شعور کو جوڑتا ہے تاکہ وہ نظام تیار کیے جا سکیں جو جسمانی تعامل کے ذریعے سیکھ سکیں۔

## باب 2: ہیومنوائڈ روبوٹکس کی ڈیزائن

ہیومنوائڈ روبوٹس انسانی شکل اور رویّے کو نقل کرنے کے لیے ڈیزائن کیے گئے ہیں۔ اہم اجزاء میں شامل ہیں:

- **اکچو ایٹرز**: حرکت کو فعال کرنے والے موتور سسٹم
- **سینسرز**: ادراک کے لیے کیمرے، مائیکروفونز، اور چھونے والے سینسرز
- **کنٹرول سسٹم**: حرکت اور رویّے کو منظم کرنے والے الگورتھم
- **سیکھنے کے نظام**: ای آئی جو تجربے کی بنیاد پر مطابقت پذیر ہوتا ہے

## باب 3: جسمانی ایجنٹس کے لیے کنٹرول سسٹم

جسمانی نظام کا مؤثر کنٹرول ایسے الگورتھم کا تقاضا کرتا ہے جو حقیقی وقت کی پابندیوں، عدم یقینی، اور متحرک ماحول کو سنبھال سکے۔ جدید طریقے کلاسیکل کنٹرول تھیوری اور مشین لرننگ کو جوڑتے ہیں۔

## باب 4: سینسر انٹیگریشن اور ادراک

روبوٹس کو اپنے ماحول کو سمجھنے کے لیے پیچیدہ حسی ڈیٹا کی تشریح کرنی ہوتی ہے۔ اس میں کمپیوٹر وژن، آڈیو پروسیسنگ، اور متعدد حسی فیوژن تکنیک شامل ہیں۔

## باب 5: موشن پلاننگ اور کنٹرول

متحرک ماحول میں پیچیدہ حرکات کی منصوبہ بندی ایسے الگورتھم کا تقاضا کرتی ہے جو فزکس، رکاوٹوں، اور اہداف کے بارے میں حقیقی وقت میں استدلال کر سکتے ہیں۔

## باب 6: جسمانی نظاموں میں سیکھنا

فزیکل ای آئی نظام اپنے ماحول کے ساتھ تعامل کے ذریعے سیکھتے ہیں، جسمانیات، سہولت فراہم کرنے، اور سبب و اثر کے تعلقات کے نمونے تجربے کے ذریعے تیار کرتے ہیں۔

## باب 7: اطلاقیہ اور مستقبل کی سمتیں

فزیکل ای آئی کے مینوفیکچرنگ، ہیلتھ کیئر، امدادی ٹیکنالوجی، اور تلاش کے شعبوں میں اطلاقیہ ہیں۔ مستقبل میں زیادہ قابل اور خود مختار جسمانی نظام کا وعدہ کرتا ہے۔`);
        } else {
          setBookContent(englishContent);
        }
      }
    } catch (err) {
      // If there's an error, provide sample content in English
      if (language === 'ur') {
        setBookContent(`# فزیکل ای آئی اور ہیومنوائڈ روبوٹکس: ڈیجیٹل دماغ اور جسمانی سریلے کو ملانا

## باب 1: فزیکل ای آئی کا تعارف

فزیکل ای آئی مصنوعی ذہانت میں ایک نظریاتی بدلاؤ کی نمائندگی کرتا ہے، جہاں ذہین نظام جسمانی اشکال میں جاری کیے جاتے ہیں جو حقیقی دنیا کے ساتھ تعامل کرتے ہیں۔ یہ مشین لرننگ، روبوٹکس، اور جسمانی شعور کو جوڑتا ہے تاکہ وہ نظام تیار کیے جا سکیں جو جسمانی تعامل کے ذریعے سیکھ سکیں۔

## باب 2: ہیومنوائڈ روبوٹکس کی ڈیزائن

ہیومنوائڈ روبوٹس انسانی شکل اور رویّے کو نقل کرنے کے لیے ڈیزائن کیے گئے ہیں۔ اہم اجزاء میں شامل ہیں:

- **اکچو ایٹرز**: حرکت کو فعال کرنے والے موتور سسٹم
- **سینسرز**: ادراک کے لیے کیمرے، مائیکروفونز، اور چھونے والے سینسرز
- **کنٹرول سسٹم**: حرکت اور رویّے کو منظم کرنے والے الگورتھم
- **سیکھنے کے نظام**: ای آئی جو تجربے کی بنیاد پر مطابقت پذیر ہوتا ہے

## باب 3: جسمانی ایجنٹس کے لیے کنٹرول سسٹم

جسمانی نظام کا مؤثر کنٹرول ایسے الگورتھم کا تقاضا کرتا ہے جو حقیقی وقت کی پابندیوں، عدم یقینی، اور متحرک ماحول کو سنبھال سکے۔ جدید طریقے کلاسیکل کنٹرول تھیوری اور مشین لرننگ کو جوڑتے ہیں۔

## باب 4: سینسر انٹیگریشن اور ادراک

روبوٹس کو اپنے ماحول کو سمجھنے کے لیے پیچیدہ حسی ڈیٹا کی تشریح کرنی ہوتی ہے۔ اس میں کمپیوٹر وژن، آڈیو پروسیسنگ، اور متعدد حسی فیوژن تکنیک شامل ہیں۔

## باب 5: موشن پلاننگ اور کنٹرول

متحرک ماحول میں پیچیدہ حرکات کی منصوبہ بندی ایسے الگورتھم کا تقاضا کرتی ہے جو فزکس، رکاوٹوں، اور اہداف کے بارے میں حقیقی وقت میں استدلال کر سکتے ہیں۔

## باب 6: جسمانی نظاموں میں سیکھنا

فزیکل ای آئی نظام اپنے ماحول کے ساتھ تعامل کے ذریعے سیکھتے ہیں، جسمانیات، سہولت فراہم کرنے، اور سبب و اثر کے تعلقات کے نمونے تجربے کے ذریعے تیار کرتے ہیں۔

## باب 7: اطلاقیہ اور مستقبل کی سمتیں

فزیکل ای آئی کے مینوفیکچرنگ، ہیلتھ کیئر، امدادی ٹیکنالوجی، اور تلاش کے شعبوں میں اطلاقیہ ہیں۔ مستقبل میں زیادہ قابل اور خود مختار جسمانی نظام کا وعدہ کرتا ہے۔`);
      } else {
        setBookContent(`# Physical AI & Humanoid Robotics: Bridging the Digital Brain and the Physical Body

## Chapter 1: Introduction to Physical AI

Physical AI represents a paradigm shift in artificial intelligence, where cognitive systems are embodied in physical forms that interact with the real world. This field combines machine learning, robotics, and embodied cognition to create systems that learn through physical interaction.

## Chapter 2: Humanoid Robotics Design

Humanoid robots are designed to mimic human form and behavior. Key components include:

- **Actuators**: Motor systems that enable movement
- **Sensors**: Cameras, microphones, and tactile sensors for perception
- **Control Systems**: Algorithms that coordinate movement and behavior
- **Learning Systems**: AI that adapts based on experience

## Chapter 3: Control Systems for Physical Agents

Effective control of physical systems requires sophisticated algorithms that can handle real-time constraints, uncertainty, and dynamic environments. Modern approaches combine classical control theory with machine learning.

## Chapter 4: Sensor Integration and Perception

Robots must interpret complex sensory data to understand their environment. This involves computer vision, audio processing, and multi-sensor fusion techniques.

## Chapter 5: Motion Planning and Control

Planning complex movements in dynamic environments requires sophisticated algorithms that can reason about physics, obstacles, and goals in real-time.

## Chapter 6: Learning in Physical Systems

Physical AI systems learn through interaction with their environment, building models of physics, affordances, and causal relationships through experience.

## Chapter 7: Applications and Future Directions

Physical AI has applications in manufacturing, healthcare, assistive technology, and exploration. The future promises increasingly capable and autonomous embodied systems.`);
      }
      console.error('Error fetching book content:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    // Re-fetch content when language changes
    fetchBookContent();
  };

  return (
    <Layout title="Book Content" description="Read the Physical AI & Humanoid Robotics book in English or Urdu">
      <div style={{ padding: '2rem', minHeight: '80vh' }}>
        <div className="container">
          <div className="row">
            <div className="col col--12">
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1.5rem',
                padding: '1rem',
                backgroundColor: '#f3f4f6',
                borderRadius: '0.5rem'
              }}>
                <h1 style={{ margin: 0 }}>Book Content</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  <button
                    onClick={() => handleLanguageChange('en')}
                    style={{
                      padding: '0.5rem 1rem',
                      backgroundColor: language === 'en' ? '#2563eb' : '#e5e7eb',
                      color: language === 'en' ? 'white' : '#374151',
                      border: '1px solid #d1d5db',
                      borderRadius: '0.375rem',
                      cursor: 'pointer'
                    }}
                  >
                    English
                  </button>
                  <button
                    onClick={() => handleLanguageChange('ur')}
                    style={{
                      padding: '0.5rem 1rem',
                      backgroundColor: language === 'ur' ? '#2563eb' : '#e5e7eb',
                      color: language === 'ur' ? 'white' : '#374151',
                      border: '1px solid #d1d5db',
                      borderRadius: '0.375rem',
                      cursor: 'pointer'
                    }}
                  >
                    Urdu
                  </button>
                </div>
              </div>

              {error && (
                <div style={{
                  padding: '1rem',
                  backgroundColor: '#fee2e2',
                  color: '#dc2626',
                  borderRadius: '0.375rem',
                  marginBottom: '1rem'
                }}>
                  {error}
                </div>
              )}

              {isLoading ? (
                <div style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: '200px',
                  fontSize: '1.2rem'
                }}>
                  Loading book content...
                </div>
              ) : (
                <div style={{
                  padding: '1.5rem',
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                  lineHeight: '1.8',
                  minHeight: '400px'
                }}>
                  {bookContent && (
                    <div style={{
                      direction: language === 'ur' ? 'rtl' : 'ltr',
                      textAlign: language === 'ur' ? 'right' : 'left',
                      fontSize: language === 'ur' ? '1.2rem' : '1rem'
                    }}>
                      {bookContent}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default BookContent;