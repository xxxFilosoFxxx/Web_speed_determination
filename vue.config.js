module.exports = {
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
  chainWebpack: (config) => {
    config
        .plugin('html')
        .tap((args) => {
          args[0].title = 'Speed detection';
          return args;
        });
  },
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  },
  transpileDependencies: [
    'quasar'
  ]
}
