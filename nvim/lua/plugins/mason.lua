return {
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end
  },
  {
    "williamboman/mason-lspconfig.nvim",
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = {"lua_ls","pylsp","texlab","fortls"}
      })
    end
  },
  {
    "neovim/nvim-lspconfig",
    config = function()
      vim.diagnostic.config({ virtual_text = true})


      vim.keymap.set('n','D', vim.lsp.buf.hover, {})
      vim.keymap.set('n','gd', vim.lsp.buf.definition, {})
      vim.keymap.set({'n','v'},'<leader>ca', vim.lsp.buf.code_action, {})

    end
  }
}
