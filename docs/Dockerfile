FROM node:18-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/docusaurus.config.js ./
COPY --from=builder /app/sidebars.js ./
RUN npm install --production
EXPOSE 3000
CMD ["npm", "run", "serve", "--", "--port", "3000", "--host", "0.0.0.0"]
