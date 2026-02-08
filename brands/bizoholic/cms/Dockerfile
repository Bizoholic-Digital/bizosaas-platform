FROM php:8.2-apache

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    libicu-dev \
    libxml2-dev \
    unzip \
    git \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd mysqli pdo_mysql zip opcache bcmath exif intl soap

# Enable Apache modules
RUN a2enmod rewrite

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set Apache ServerName to suppress warning
RUN echo "ServerName cms.bizoholic.net" >> /etc/apache2/apache2.conf

# Set working directory
WORKDIR /var/www/html

# Copy CMS files specifically
COPY . ./

# Install Composer dependencies
RUN composer install --no-dev --no-interaction --no-scripts --no-progress --optimize-autoloader

# Set up environment
RUN chown -R www-data:www-data /var/www/html

# Point DocumentRoot to web/
ENV APACHE_DOCUMENT_ROOT /var/www/html/web
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Expose port 80
EXPOSE 80

# Start Apache
CMD ["apache2-foreground"]
