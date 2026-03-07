// Placeholder for i18n configuration
// Will be implemented in Phase 6: Multilingual Support

export const supportedLanguages = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'हिन्दी' },
  { code: 'ta', name: 'தமிழ்' },
  { code: 'te', name: 'తెలుగు' },
  { code: 'bn', name: 'বাংলা' },
];

export const getCurrentLanguage = (): string => {
  return localStorage.getItem('language') || 'en';
};

export const setLanguage = (languageCode: string): void => {
  localStorage.setItem('language', languageCode);
};
