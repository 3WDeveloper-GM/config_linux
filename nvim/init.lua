local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
require("options")

vim.opt.rtp:prepend(lazypath)


require("lazy").setup("plugins")
require("keymaps")
require("lsp")


vim.cmd("hi Normal guibg=NONE ctermbg=NONE") --makes the background transparent
vim.cmd("hi NormalNC guibg=NONE ctermbg=NONE") --makes all the splits transparent
