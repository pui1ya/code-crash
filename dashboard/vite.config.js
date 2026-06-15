
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({

    plugins: [
        react()
    ],

    resolve: {

        alias: {

            "@": path.resolve(
                __dirname,
                "./src"
            ),

            "@components": path.resolve(
                __dirname,
                "./src/components"
            ),

            "@pages": path.resolve(
                __dirname,
                "./src/pages"
            ),

            "@api": path.resolve(
                __dirname,
                "./src/api"
            ),

            "@hooks": path.resolve(
                __dirname,
                "./src/hooks"
            )
        }
    },

    server: {

        host: "0.0.0.0",

        port: 3000,

        open: true,

        proxy: {

            "/api": {

                target:
                    "http://localhost:8000",

                changeOrigin: true,

                secure: false,

                rewrite: (path) =>
                    path.replace(
                        /^\/api/,
                        ""
                    )
            }
        }
    },

    preview: {

        host: "0.0.0.0",

        port: 3000
    },

    build: {

        outDir: "dist",

        sourcemap: true,

        emptyOutDir: true
    }
});
