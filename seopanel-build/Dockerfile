FROM php:8.1-apache

# Install dependencies and PHP extensions
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    libcurl4-openssl-dev \
    unzip \
    wget \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) mysqli gd zip curl

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Set working directory
WORKDIR /var/www/html

# Download and extract SEO Panel
# Using the SourceForge direct link with -L to follow redirects
RUN wget -L -O seopanel.zip https://sourceforge.net/projects/seopanel/files/seopanel.v.5.1.0.zip/download \
    && unzip seopanel.zip \
    && mv seopanel/* . \
    && rm -rf seopanel seopanel.zip

# Set permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80
