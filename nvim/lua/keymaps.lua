local map = vim.keymap.set
local opts = { noremap = true, silent = true }

local builtin = require("telescope.builtin")
map("n", "<leader>ff", builtin.find_files, opts)
map("n", "<leader>fg", builtin.live_grep, opts)
map("n", "<leader>sf", ":Neotree toggle<CR>", opts)
map("n", "<leader>nw", "<c-w><c-w>", opts)
map({ "n", "x" }, "<c-l>", "$", opts)
map("n", "<leader>clt", ":term pdflatex -interaction=nonstopmode -output-directory=compiled %<CR>", opts)
map("n", "<c-.>", "<c-6>", opts)
map("n", "<c-j>", "<c-U>", opts)
map("n", "<c-k>", "<c-D>", opts)
