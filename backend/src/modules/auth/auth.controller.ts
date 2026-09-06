import { Controller, Post, Get, Body, Headers } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('Authentication & Roles')
@Controller('api/v1/auth')
export class AuthController {
  @Post('login')
  @ApiOperation({ summary: 'Login with username/password or mobile OTP' })
  login(@Body() body: any) {
    const isInspector = body.username?.includes('inspector') || body.role === 'INSPECTOR';
    const role = isInspector ? 'INSPECTOR' : 'BUSINESS';
    
    return {
      user: {
        id: `usr_${Date.now()}`,
        name: body.username || 'Demo User',
        email: body.email || 'user@example.gov.in',
        phone: body.phone || '+91-9876543210',
        role: role,
        isInspector: isInspector,
        isBusiness: !isInspector,
        keycloakId: `kc_${Date.now()}`,
      },
      tokens: {
        accessToken: `mock_jwt_access_token_${Date.now()}`,
        refreshToken: `mock_jwt_refresh_token_${Date.now()}`,
        expiresIn: 3600,
      },
      accessToken: `mock_jwt_access_token_${Date.now()}`,
      refreshToken: `mock_jwt_refresh_token_${Date.now()}`,
    };
  }

  @Post('register/business')
  @ApiOperation({ summary: 'Register a new business account' })
  registerBusiness(@Body() body: any) {
    return {
      id: `usr_${Date.now()}`,
      name: body.fullName || body.username || 'New Business Owner',
      email: body.email,
      phone: body.phone,
      role: 'BUSINESS',
      isBusiness: true,
      isInspector: false,
    };
  }

  @Post('register')
  @ApiOperation({ summary: 'Register a new citizen/user account' })
  register(@Body() body: any) {
    return {
      id: `usr_${Date.now()}`,
      name: body.name || 'New User',
      email: body.email,
      role: body.role || 'CITIZEN',
    };
  }

  @Post('refresh')
  @ApiOperation({ summary: 'Refresh access token' })
  refresh(@Body() body: any) {
    return {
      accessToken: `mock_jwt_access_token_refreshed_${Date.now()}`,
      refreshToken: body.refreshToken || `mock_jwt_refresh_token_${Date.now()}`,
      expiresIn: 3600,
    };
  }

  @Get('me')
  @ApiOperation({ summary: 'Get current authenticated user profile' })
  me(@Headers('authorization') authHeader: string) {
    return {
      id: 'usr_current',
      name: 'Legal Metrology Officer',
      email: 'officer@legalmetrology.maharashtra.gov.in',
      role: 'INSPECTOR',
      isInspector: true,
      isBusiness: false,
    };
  }

  @Post('logout')
  @ApiOperation({ summary: 'Logout current user' })
  logout() {
    return { status: 'SUCCESS', message: 'Logged out successfully' };
  }
}
