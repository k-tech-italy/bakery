module.exports = {
  purge: [
    './src/{{cookiecutter.project__slug}}/web/templates/**/*.html'
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
};
