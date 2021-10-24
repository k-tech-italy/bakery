const path = require('path');

const webDir = path.resolve(__dirname, "./src/{{cookiecutter.project__slug}}/web");
const assetsDir = path.resolve(webDir, "./assets");
const staticDir = path.resolve(webDir, "./static");


module.exports = {
  entry: path.resolve(assetsDir, './js/app.js'),
  output: {
    path: path.resolve(staticDir, './js'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/i,
        include: assetsDir,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/i,
        include: assetsDir,
        exclude: /node_modules/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  'postcss-preset-env',
                ],
              },
            },
          },
        ],
      },
    ],
  },
};
