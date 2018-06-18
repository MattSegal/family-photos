const path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: [
    './frontend/index.js'
  ],
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: true,
              localIdentName: '[name]__[local]___[hash:base64:5]'
            }
          },
        ]
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: [
      '/app/frontend',
      '/app/node_modules'
    ]
  },
  plugins: [
    new BundleTracker({filename: 'webpack-stats.json'})
  ]
};
