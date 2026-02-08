"use client";

import React from "react";
import { useAuth } from "@/shared/components/AuthProvider";
import { getEffectivePermissions, RolePermissions } from "@/lib/rbac";

interface PermissionGuardProps {
    permission: keyof RolePermissions;
    children: React.ReactNode;
    fallback?: React.ReactNode;
}

/**
 * A component that only renders its children if the user has the required permission.
 * Considers both User Role and Lago Plan Features.
 */
export function PermissionGuard({
    permission,
    children,
    fallback = null,
}: PermissionGuardProps) {
    const { user } = useAuth();

    if (!user) return <>{fallback}</>;

    const effectivePermissions = getEffectivePermissions(
        (user.role as any) || "user",
        user.plan_features || []
    );

    if (effectivePermissions[permission]) {
        return <>{children}</>;
    }

    return <>{fallback}</>;
}
