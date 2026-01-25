# Lago Admin User Creation - Step by Step
**Date**: 2026-01-25 08:57 UTC

You are currently in the Rails console. Follow these steps:

---

## Step 1: Create Organization

Paste this command:

```ruby
org = Organization.find_or_create_by!(name: 'Bizoholic')
```

**Expected Output**: Should return the organization object

---

## Step 2: Create User

Paste this command:

```ruby
user = User.find_or_initialize_by(email: 'admin@bizoholic.net')
```

**Expected Output**: Should return a user object (may be new or existing)

---

## Step 3: Set Password

Paste these commands one by one:

```ruby
user.password = 'Password123!'
user.password_confirmation = 'Password123!'
user.save!
```

**Expected Output**: Should return `true` after `save!`

---

## Step 4: Create Admin Membership

Paste this command:

```ruby
membership = Membership.find_or_create_by!(user: user, organization: org, role: :admin)
```

**Expected Output**: Should return the membership object

---

## Step 5: Verify Creation

Paste this command to verify:

```ruby
puts "\n✅ Admin user created successfully!"
puts "Email: #{user.email}"
puts "Organization: #{org.name}"
puts "Role: #{membership.role}"
puts "User ID: #{user.id}"
```

**Expected Output**: 
```
✅ Admin user created successfully!
Email: admin@bizoholic.net
Organization: Bizoholic
Role: admin
User ID: [some number]
```

---

## Step 6: Exit Rails Console

Type:

```ruby
exit
```

---

## Step 7: Test Login

1. Open browser: https://billing.bizoholic.net
2. Login with:
   - Email: `admin@bizoholic.net`
   - Password: `Password123!`

---

## Alternative: All-in-One Command

If you prefer, you can paste this entire block at once:

```ruby
org = Organization.find_or_create_by!(name: 'Bizoholic')
user = User.find_or_initialize_by(email: 'admin@bizoholic.net')
user.password = 'Password123!'
user.password_confirmation = 'Password123!'
user.save!
membership = Membership.find_or_create_by!(user: user, organization: org, role: :admin)
puts "\n✅ Admin user created successfully!"
puts "Email: #{user.email}"
puts "Organization: #{org.name}"
puts "Role: #{membership.role}"
puts "User ID: #{user.id}"
```

---

## Troubleshooting

### If you get "Organization not found" error:
The Organization model might not exist. Try:
```ruby
Organization.create!(name: 'Bizoholic')
```

### If you get "User validation failed":
Check what validations failed:
```ruby
user.errors.full_messages
```

### If password is too short:
Lago might require a longer password. Try:
```ruby
user.password = 'BizoholicAdmin2025!'
user.password_confirmation = 'BizoholicAdmin2025!'
user.save!
```

---

**Current Status**: You are in Rails console, ready to execute commands!
