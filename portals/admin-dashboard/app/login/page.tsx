import { signIn } from "@/lib/auth";
import { UnifiedLoginForm } from "@bizosaas/shared-ui";
import { PlatformBranding } from "@/components/ui/platform-branding";

export default function AdminLoginPage({
  searchParams,
}: {
  searchParams: { callbackUrl?: string };
}) {
  return (
    <UnifiedLoginForm
      mode="sso"
      platformName="Admin Dashboard"
      platformSubtitle="Platform Administration & Management"
      ssoProviderName="Authentik"
      ssoProviderId="authentik"
      defaultRedirectUrl="/dashboard"
      BrandingComponent={() => <PlatformBranding platform="BIZOSAAS" size="lg" />}
      onSSOLogin={async () => {
        "use server";
        await signIn("authentik", {
          redirectTo: searchParams.callbackUrl || "/dashboard",
        });
      }}
    />
  );
}