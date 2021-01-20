module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: {
        // "class-name : 적용할 css값"
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh"
      },
      borderRadius: {
        xl: "1.5rem"
      },
      minHeight: {
        "50vh": "50vh",
        "75vh": "75vh"
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
