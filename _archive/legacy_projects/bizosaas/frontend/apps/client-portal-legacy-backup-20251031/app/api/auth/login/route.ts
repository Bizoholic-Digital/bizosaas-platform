import { NextRequest, NextResponse } from "next/server";

// Demo users for development
const DEMO_USERS = {
  "demo@bizosaas.com": {
    id: "user_demo_001",
    email: "demo@bizosaas.com", 
    password: "demo123",
    name: "Demo User",
    role: "admin",
    tenant_id: "tenant_demo"
  }
};

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password } = body;

    // Check demo credentials
    const user = DEMO_USERS[email as keyof typeof DEMO_USERS];
    
    if (!user || user.password !== password) {
      return NextResponse.json({
        success: false,
        error: "Invalid email or password"
      }, { status: 401 });
    }

    // Generate simple token (for demo purposes)
    const tokenData = {
      user_id: user.id,
      email: user.email,
      tenant_id: user.tenant_id,
      exp: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
    };
    
    const token = Buffer.from(JSON.stringify(tokenData)).toString("base64");

    return NextResponse.json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        tenant_id: user.tenant_id
      }
    });

  } catch (error) {
    console.error("Login error:", error);
    return NextResponse.json({
      success: false,
      error: "Authentication service error"
    }, { status: 500 });
  }
}
