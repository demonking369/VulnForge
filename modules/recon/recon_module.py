import asyncio
from typing import List


class ReconModule:
    async def discover_subdomains(self, target: str) -> List[str]:
        """Discover subdomains using subfinder"""
        try:
            # Extract domain from URL if needed
            domain = target.split("://")[-1].split("/")[0]

            # First check if it's an S3-hosted domain
            s3_check = await self._run_command(f"dig +short -t NS {domain}")
            if "s3" in s3_check.lower():
                self.logger.info(f"Domain {domain} appears to be S3-hosted")
                return [domain]  # Return main domain for S3-hosted sites

            # Run subfinder with passive sources
            cmd = [
                "subfinder",
                "-d",
                domain,
                "-silent",
                "-sources",
                "crtsh,alienvault,hackertarget,digitorus,anubis",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if stderr:
                self.logger.warning(f"Subfinder stderr: {stderr.decode()}")

            if not stdout:
                self.logger.warning(
                    f"No output from subfinder for {domain}. Check if subfinder is installed and configured correctly."
                )
                print(
                    f"Warning: No output from subfinder for {domain}. Check if subfinder is installed and configured correctly."
                )
                return [domain]  # Return main domain if no subdomains found

            # Process output
            subdomains = [
                line.strip() for line in stdout.decode().splitlines() if line.strip()
            ]

            if not subdomains:
                self.logger.warning(
                    f"No subdomains found for {domain}. Check subfinder installation, network, and API keys."
                )
                print(
                    f"Warning: No subdomains found for {domain}. Check subfinder installation, network, and API keys."
                )
                return [domain]  # Return main domain if no subdomains found

            # Add main domain if not in list
            if domain not in subdomains:
                subdomains.append(domain)

            return subdomains

        except Exception as e:
            self.logger.error(f"Error discovering subdomains: {str(e)}")
            return [
                target.split("://")[-1].split("/")[0]
            ]  # Return main domain on error
