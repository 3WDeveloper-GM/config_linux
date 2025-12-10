local capabilities = require("cmp_nvim_lsp").default_capabilities()

local lsp_o = vim.lsp

lsp_o.enable("luals")
lsp_o.enable("pyright")
lsp_o.enable("texlab")

lsp_o.config("luals", {
	capabilities = capabilities,
	cmd = { "lua-language-server" },
	filetypes = { "lua" },
	settings = {
		Lua = { diagnostics = { globals = { "vim" } } },
	},
})
lsp_o.config("pyright", {
	capabilities = capabilities,
	cmd = { "pyright-langserver", "--stdio" },
	filetypes = { "python" },
	root_markers = {
		"pyproject.toml",
		"setup.py",
		"setup.cfg",
		"requirements.txt",
		"Pipfile",
		"pyrightconfig.json",
		".git",
	},
	settings = {
		python = {
			analysis = {
				autoSearchPaths = true,
				diagnosticMode = "openFilesOnly",
				useLibraryCodeForTypes = true,
			},
		},
	},
})
lsp_o.config("texlab", {
	capabilities = capabilities,
	cmd = { "texlab" },
	filetypes = { "tex", "plaintex", "bib" },
	settings = {
  texlab = {
    bibtexFormatter = "texlab",
    build = {
      args = { "-pdf", "-interaction=nonstopmode", "-synctex=1", "%f" },
      executable = "latexmk",
      forwardSearchAfter = false,
      onSave = false
    },
    chktex = {
      onEdit = false,
      onOpenAndSave = false
    },
    diagnosticsDelay = 300,
    formatterLineLength = 80,
    forwardSearch = {
      args = {}
    },
    latexFormatter = "latexindent",
    latexindent = {
      modifyLineBreaks = false
    }
  }
}
})
