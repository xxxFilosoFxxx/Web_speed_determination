module.exports = {
  chainWebpack: (config) => {
    config
        .plugin('html')
        .tap((args) => {
          args[0].title = 'Speed detection';
          return args;
        });
  },
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
